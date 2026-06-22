# SESSION v0.9 — L8 global integration / functional access (a global metastable resonant hub that broadcasts the dominant pattern)

**Module:** `repro/wave_workspace_core.py` (reuses L0 `wave_compute_core` — `hebbian_field`,
`relax` clean-up = D4 noise immunity, `overlap`, `pattern_to_phase`, `corrupt_phase`, `global_R`
— and the L3 selection mechanism `wave_hierarchy_core.gate_weights` — the von Mises slow-phase
GATE that here selects which MODULE wins access to the hub; exact, non-circular; nothing frozen
or prior edited; broadcast is always read at a module that did NOT hold the content, and the
PCI-analog is read on the modules downstream of a hub kick, never on the gate itself).
**Figure:** `repro/wave_workspace_atlas.png` (4 panels). **Digest:** `52a0ce34b54fc791…`
(deterministic, bit-for-bit, single-core OpenBLAS). **Firewall:** `consciousness_claim = 0`,
`hard_problem_open = 1`. **`new_tuned_constants = 0`.**

**Concept DOI:** `10.5281/zenodo.20783570` (reflected in `CITATION.cff` and the doc tops).

---

## Why this session

L0–L7 gave the substrate storage, an algebra, metastable trajectories, hierarchy, resonance
inference, two complementary stores, a self-supervised forward model, and a closed real-time
control loop — but each capability sits in its **own** field. A brain reaches general function
only when these specialised processes can **share**: a momentarily dominant pattern is made
**globally available** so any process can use it (Baars/Dehaene "global workspace"; the access
signature is the **PCI** of Casali/Massimini — perturb, then measure the algorithmic complexity
of the **integrated-yet-differentiated** response). L8's job (BLUEPRINT §10, §12) is to build
that sharing on the wave substrate: a **global metastable RESONANT HUB**. When a module's pattern
**resonance-LOCKS** into the hub, the hub **BROADCASTS** it back to every module, so it becomes
available system-wide. The milestone: **a hub that selectively binds the dominant module pattern
and broadcasts it system-wide, flexibly routing among modules**, with a **functional PCI-analog**
that separates engaged from disengaged, swept over module count and load, and a stress test
designed to break it.

L8 inherits L7's honest **operating-band** limit as a binding caveat: a global hub must route
among modules **within** their bandwidth/latch bands. G4 makes that concrete for the hub.

The **firewall** is re-affirmed in the only sense that matters here: **"access" is the FUNCTIONAL
sense — broadcast AVAILABILITY of a pattern to the whole system.** *Feeling* / phenomenal
experience is **not** claimed and **not** measured, in any regime, including the high-PCI engaged
one. A high functional-PCI-analog is a high **integration-and-differentiation of broadcast
information**, nothing more.

---

## The wave mechanism (entirely on L0 + the L3 gate, non-circular)

- **MODULES** — `M` populations, each an L0 attractor field that knows the shared concept
  vocabulary `V` (its clean-up field `J_mod = hebbian_field(V)`), each currently **LATCHED** on
  its own distinct concept (the stand-in for a specialised L1–L7 process holding its current
  content). Vocabulary load is kept **within** the proven L0 storage band (`N = 128`, `D ≤ 8`,
  `α ≈ D/N ≤ 0.06`), so a locking failure is never an L0-capacity artefact.
- **HUB** — one population with its **own** clean-up field `J_hub = hebbian_field(V)`, so it does
  not sit at a blur of all modules — it falls (**RESONANCE-LOCKS**) into the nearest **valid**
  concept attractor, i.e. the selected one.
- **GATE** — the L3 von Mises slow phase selects **which** module drives the hub (bottom-up
  weight `w_m` over structural addresses `φ_m = 2πm/M`). A sharp gate → one module wins.
- **BIND** — bottom-up: module `m` pulls the hub with strength `w_m` (Kuramoto coupling).
- **BROADCAST** — top-down: the locked hub pulls **every** module. A receiver that did not hold
  the content settles to it from the broadcast **alone** → global access.
- **CLOCK-FREE** — the whole hub+modules system advances by **one joint relaxation** (P2). No
  clock. The coupling form is the physics `1/r²` near-field (P3).
- **REGIME** — a single knob `g_hub` scales the hub↔module coupling: `g_hub = 0` → **ISOLATED**
  (no integration); intermediate → **ENGAGED** (the metastable operating point); `g_hub` large →
  **OVER-DRIVEN** (global sync, one state, no differentiation). The access point is read off the
  sweep — **the inherited NUMBER `R = 0.39` is NOT transferred, only the band principle.**

---

## What was built and found (each claim with a sweep; honest negatives kept)

### G1 — selective access + global broadcast  **[V]**  (the L8 milestone, part 1)
`M` modules each hold a distinct concept; the gate selects module `k`. Sweep `M ∈ {3,4,6,8}` ×
vocabulary `D ∈ {6,8}` × seeds. The hub **resonance-LOCKS** to module `k`'s concept with a large
margin (overlap with the selected concept minus the mean of the others **≥ 0.92** every config;
`hub_locks_selected = 1.00`), and a **NON-SOURCE** receiver module `r ≠ k` — after its own
content is **erased** — recovers concept `k` from the **broadcast alone** (`broadcast_recall_
receiver = 1.00` every config), where a **no-hub control** (coupling 0) is at chance
(`0.00 – 0.33 ≈ 1/M`). **The verified claim:** the gate **selects** one module, the hub binds
**that** concept (it does not blur all modules together), and the bound pattern becomes **globally
available** — a module that never held it reads it off the hub. The stress ("binds all modules
equally OR a non-source module cannot read the broadcast") **did not fire**.

### G2 — flexible routing  **[V]**  (the L8 milestone, part 2)
Broadcast a **sequence** of targets by moving the gate; routing accuracy = fraction of steps whose
broadcast content equals the intended module's concept. Sweep `M ∈ {3,4,6,8}` × number of routes
`∈ {6,10}` × seeds. **Flexible** routing is **perfect** (`1.00` every config) while a **fixed**
gate (frozen on module 0) reaches only its own module (`0.03 – 0.32 ≈ 1/M`), beating the fixed
gate by `> 0.2` everywhere, sign-stable. **The verified claim:** moving the gate **routes any
module's content** to the whole system — the workspace is **reconfigurable**, not hard-wired. The
stress ("routing is hard-wired / cannot reconfigure") **did not fire**.

### G3 — functional PCI-analog: engaged vs disengaged  **[V]**  (borrowing Gap-4; the access signature)
**The measure.** The functional PCI-analog as **integration × differentiation** — faithful to the
Casali/Massimini PCI logic (an **integrated AND differentiated** response is high) with **no
Lempel-Ziv parse and no critical-point tuning**. The hub is first locked to the gated concept
**without broadcasting** (`kdown = 0`), so the modules keep their **own distinct** contents (a
broadcasting lock-in would pre-collapse every module onto one concept and kill differentiation
before the sweep even starts). Then at each coupling `g_hub` the hub is **kicked** and a matched
**no-kick** reference is run from the same state; the modules are read (non-circular: kick the
hub, measure the modules):
- **INTEGRATION** `I(g)` = how far the perturbation **SPREADS** into the modules, over the whole
  **evoked trajectory** (not the endpoint, which a stable attractor re-absorbs) = mean
  significant-activity (fraction of (module, time, oscillator) cells where the kicked run differs
  from the no-kick run). **`I(0) = 0` exactly** (at `g = 0` the modules are decoupled from the
  hub, so the two runs are byte-identical); `I` rises as coupling carries the kick in.
- **DIFFERENTIATION** `D(g)` = how **DISTINCT** the kicked modules' contents remain = mean
  pairwise normalised Hamming among the kicked module final states. High while modules keep their
  own concepts; **`D → 0`** once a strong broadcast collapses them all onto the single hub concept.
- **PCI(g) = I(g) · D(g)** → `0` at **ISOLATED** (`I = 0`), `→ 0` at **OVER-DRIVEN** (`D → 0`),
  and **PEAKS** at the metastable **ENGAGED** edge where the perturbation both spreads and the
  modules stay differentiated.

**Found.** Sweep `g_hub ∈ {0, 0.25, 0.5, 1, 2, 4, 8}` × `M ∈ {4,6,8}` × seeds. The curve is a
clean **inverted-U**: at `g = 0` PCI `= 0.000` (`I = 0`, `D ≈ 0.50`); the **emergent access peak**
is **interior** (`g = 0.5` for `M = 4,6`, `g = 0.25` for `M = 8`; PCI `0.021 / 0.022 / 0.040`);
by `g = 1` the modules have collapsed (`D ≈ 0.00`, PCI `≈ 0.000`) and it stays `0` through
`g = 8`. The **integration term rises** while the **differentiation term falls** — their crossover
**is** the access band. The engaged peak exceeds **both** the isolated floor and the over-driven
ceiling at every `M`, and is **interior** at every `M`. **The verified claim:** there is a
**functional access signature** — an integrated-and-differentiated broadcast response that is high
only at the metastable edge, exactly the inherited **Gap-4 inverted-U**. **The access point is
read off the sweep; the NUMBER `R = 0.39` is not transferred.** The stress ("engaged does not
exceed both disengaged regimes / no interior peak") **did not fire.** **FIREWALL banner emitted:**
functional broadcast complexity only — no felt experience is claimed in any regime, including the
high-PCI engaged one.

### G4 — the inherited operating-band limit  **[V] band / [O] unbounded-rate**  (L7's open limit, made concrete; honest)
Route a sequence of targets while sweeping the **DWELL** = settle-steps the hub is allowed before
the gate switches. **Each routing operation is a FRESH IGNITION** (the modules are pristine and
the hub is un-committed), so the dwell controls exactly one thing: whether the hub is given enough
time to **resonance-LOCK** onto the gated target before it must move on. Sweep
`dwell ∈ {2,5,10,20,40,80,160}` × seeds. Below the hub's **LOCK LATENCY** the gate re-routes
faster than the hub can latch and routing **collapses** toward chance (`dwell 2 → 0.25`,
`5 → 0.54`, `10 → 0.73`, chance `1/M = 0.17`); at or above it routing **holds** (`20 → 0.96`,
`40/80/160 → 1.00`). The **band edge** (smallest dwell that holds) is **`20` settle-steps** — the
operating-band limit, the L8 instance of the inherited L7 caveat that the hub must route **within**
its own latch band. **The verified claim:** a **non-empty within-band regime where routing holds**
exists, and its edge is the recorded honest limit; **unbounded-rate routing is impossible [O]**.

**Honest negative (recorded, not hidden):** a hub that instead **carries** its previous committed
concept forward (no re-cue) is **not reliably re-routable** by the gate at the substrate coupling
`g_hub = 1` — once latched on concept A, the gate's pull toward B often cannot dislodge it, and
**more** dwell makes it **worse** (it drifts deeper): given **4× the longest sweep dwell**
(`640` steps) it reaches only `0.71`, while the re-cued band saturates at `1.00`. Sequential
access on this substrate therefore **favours a fresh ignition per route** (the previous content
must release first); **persistent over-write routing is an open limit [O].** The stress ("modules
don't integrate / no flexible routing") **did not break the path** — it **bounds** it.

---

## L8 verdict (honestly)

**The substrate integrates its specialised modules into a global workspace.** A global metastable
resonant hub **selectively binds** the gated module's pattern and **broadcasts** it so a module
that never held it recovers it (G1 [V]); moving the gate **flexibly routes** any module's content
system-wide where a fixed gate cannot (G2 [V]); and a **functional PCI-analog** —
integration × differentiation of the modules' response to a hub kick — is **high only at the
metastable edge**, low both isolated (no integration) and over-driven (no differentiation),
reproducing the inherited **Gap-4 inverted-U** (G3 [V]). **Three milestone capabilities [V].**
The inherited **operating-band limit is made concrete**: routing holds **within** the hub's
lock-latency band and collapses outside it (G4 band [V]), and **unbounded-rate / no-release
routing is an open limit** (G4 [O]) — recorded, not hidden.

**The access claim, bounded.** The PCI-analog is the **functional** access signature only:
broadcast **availability** that is integrated **and** differentiated. The firewall holds at every
step — **`consciousness_claim = 0`, `hard_problem_open = 1`** — including the high-PCI engaged
regime. A high functional-PCI-analog is **broadcast information made globally available and kept
distinct**, nothing more; **no felt quality is claimed or measured.**

**Discipline upheld.** Every claim swept and sign-stable; integration is **continuous settling**
on the frozen L0 substrate and selection is the **L3 gate** — no read-out is circular (broadcast
read at a **non-source** module; the PCI-analog read on the **modules** downstream of a **hub**
kick; routing scored against the **intended** concept). The regime is **swept** via `g_hub`
(reported, not tuned); gate centres are **structural**; `SETTLE` is a dynamics constant, not
fitted; the brain anchor `R = 0.39` is **not** transferred (the access point **emerges** from the
sweep); `new_tuned_constants = 0`; firewall held at every step; digest reproduces bit-for-bit on a
single core across repeated runs.

**Layer status after S9. L8 global integration / functional access — MET & GRADED.** Strongly
positive (**3/3 milestone lines [V]**: selective access + broadcast, flexible routing, functional
PCI-analog inverted-U) with the inherited operating-band limit made concrete (band [V]) and its
two honest counterpoints recorded ([O]: unbounded-rate routing; [O]: persistent no-release
over-write routing). Exposed dependency → **L9 — functional general intelligence (the end
condition)**, the final layer in the inherited chain (BLUEPRINT §11): with L0–L8 now each MET &
GRADED or recorded as an honest `[O]`, the integrated system is assessed against the **capability
ladder** — one-shot generalization, **compositional / systematic generalization**, real-time
adaptation, noise-immersed robustness, scale content-addressable memory, cross-domain transfer,
open-ended skill acquisition — each scored pass / honest-negative. Since the workspace now
broadcasts a **single** dominant pattern, the **compositional / multi-item** rung of that ladder
(holding and binding **several** broadcast items at once within the inherited theta-gamma capacity
`≈ 7` — the system-scale form of L4's binding question) is the natural first probe. **Firewall
(final):** even if every criterion passes, that is **functional** general intelligence — the
hard-problem blank stays open (`consciousness_claim = 0`, `hard_problem_open = 1`), never erased.

**Artifacts.** `wave_workspace_core.py` (+`wave_workspace_results.json`
+`wave_workspace_atlas.png` +`expected_digest_v0_9.json`), `make_figure_v0_9.py` (4-panel
G1 selective access + broadcast / G2 flexible routing / G3 the PCI-analog inverted-U with the
integration↑ × differentiation↓ crossover / G4 the lock-latency operating band + carry-forward
honest negative), `CITATION.cff` (concept DOI `10.5281/zenodo.20783570`). `check_completeness.py`
updated to re-run and pin this module. Digest `52a0ce34b54fc791…`, deterministic.
