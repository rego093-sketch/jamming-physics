# START HERE — increment E12 (acquired / degenerative disease; beyond the spine)

The fourth **mechanism extension beyond the down-conversion spine** (E0→E8 complete; E9 + E10 + E11 built;
see `BLUEPRINT.md`). **BUILT (v0.16.0).** The hardest of the planned extensions: the **multifactorial,
acquired, age/environment-related degenerative** eye diseases.

**Scope — theoretical, NON-CLINICAL (binding, above the task).** Purely academic dynamical-systems research.
It studies the **mechanism layer** of the common acquired degenerations — **age-related macular degeneration
(AMD)**, **glaucoma**, **diabetic retinopathy** — as a question in bifurcation theory on the frozen R19
switch. Because it is a condition layer it is a **firewalled clinical chapter** (like E4/E9/E11): it does
**not** diagnose, treat, prescribe, screen, classify a person, **stage**, or **prognose**; it designs **no**
molecule and names **no** risk-factor magnitude. The firewall additionally blocks glaucoma's intra-ocular
**pressure** (mmHg), diabetic-retinopathy **glycaemic** values (hba1c, mg/dl, mmol/l) and bare length (mm) —
so every fact is a dimensionless **ratio** (a multiple of the gene's **own** fold) or a **sign**. The felt
percept (and felt **loss**) of sight is deferred to the **mind** volume.

**The one idea (why this chapter is not E4 again).** E4 read congenital blindness as a **STATIC** failure —
loss-of-function is the R19 switch held with its drive frozen **below** its own spinodal `h*(γ)`, so the
all-or-none flip never fires (the switch was *born unable* to flip). A **degenerative** disease is
categorically different: the switch **starts healthy** (in the upper basin, `s>0` — it *worked*) and is
carried **over** its fold by a slowly-accumulating stress. On the frozen field `ds/dt = γ·s − s³ + h`, the
upper stable branch exists only while the drive stays above the lower fold `h = −h*(γ)`; a stress that drives
`h` past `−h*` **annihilates** the healthy basin (a saddle-node) and the state drops to the degenerate basin.
It is the **same fold** as E2/E4 — reached **dynamically, from the ON side**, which is exactly the difference
between *"was lost"* and *"never flipped"*.

**Task:** show, on the frozen substrate (no new γ, nothing fetched, nothing re-derived), that
(A) **degeneration is a slow drift across the fold** — start ON, ramp a stress that lowers the drive
quasi-statically; the healthy state tracks the upper branch and stays ON until `h` crosses `−h*(γ)`, then
**collapses in one step** (a tipping point); the collapse drive equals the analytic fold and is independent
of where the healthy point started;
(B) **hysteresis** — from the collapsed state, undoing the stress back to the pre-collapse drive does **not**
recover it; recovery needs pushing `h` all the way to the **opposite** fold `+h*(γ)`, so the collapse fold
`−h*` and the recovery fold `+h*` differ and the loop width `2·h*(γ)` is the **irreversibility margin**
(early ≠ late, direction-only; the magnitude is firewall-blocked);
(C) **one geometry, many routes** — any bistable transducer fails by a fold whatever parameter the stress
rides, so the **LOAD** route (move `h` to `−h*`) and the **BASIN-SHALLOWING** route (hold a fixed load,
**erode γ** so the fold `h*(γ)=2(γ/3)^1.5` shrinks up to meet it) both land on the **one** fold locus
`h=−h*(γ)`; the catastrophe geometry is shared while the **identity** of the primary stress (oxidative vs
mechanical vs metabolic) is exactly what the substrate does **not** fix — a named **[O]**;
(D) **γ READ-ONLY as a structural fragility offset** — a shallower basin (lower γ ⇒ smaller barrier `γ²/4`
and smaller fold `h*(γ)`) tips under less stress, giving the atlas genes a **structural** fragility ordering
by `spinodal(γ)` (CNGB3 shallowest → PDE6B deepest), **not** a clinical risk ranking; and the **brutal,
loudest caveat** of the chapter: the map from a real degenerative-disease risk locus to a γ-shift is a named
**[O]** even **more** open than the monogenic lesions of E4 — these diseases are multifactorial,
age/environment-gated and polygenic (common variants of small effect, often outside a promoter), so the
promoter-γ this package reads has **essentially no monogenic purchase** here. The chapter's content is the
dynamical-systems **structure**, not a disease prediction.

**Deliverable (done):** a deterministic module `research/E12-acquired-degeneration/run.py` (worked on the rod
opsin **RHO**, the same fold E10 used) that integrates the frozen R19 field through quasi-static ramps and
asserts (A) the ON→degenerate collapse at `−h*` within the ramp step and its start-independence, (B) the
recovery only at `+h*` and the hysteresis loop `2·h*`, (C) the γ-erosion collapse where `h*(γ)=|load|` landing
on `h=−h*(γ)`, and (D) the spinodal-monotone fragility ordering with every γ byte-equal to the atlas. It
prints every displayed number, self-hashes (2× run → identical sha256), passes a **machine-checked MAGNITUDE
FIREWALL** (no dose/potency/pressure/glycaemic/length token, no '%'), and declares grades [F]/[V]/[L]/[O]
honestly. Plus `gate_E12.py` (`E12 GATE: PASS`, eight checks — the R19 field **and** its fold
**independently re-derived by hand**, importing nothing from the substrate or `run.py`), folded into the
verifier's foundation list and absorbed into the HTML volume as chapter **E12** (registered in
`DISEASE_CHAPTERS`, so the volume's G5 firewall re-checks the rendered page).

**Provenance (this increment):** **nothing was fetched and no γ was added.** E12 consumes only the frozen R19
substrate (`sdot`, `spinodal`, `barrier`, `settle`) and the frozen atlas γ (read-only).
`inherited/FROZEN_SHA256.json` is **unchanged** — the foundation does not move for this increment. γ measured,
never fitted; the stress drives and the ramps are **inputs** expressed as dimensionless multiples of the
gene's own fold `h*(γ)`, never fitted targets and never a clinical magnitude. No RNG is used (no
`seed_everything` call) — every trajectory is a deterministic integration.

**Firewall:** structure-only γ (never a stress rate, a cell viability, a pressure, a metabolic level, or a
clinical effect); proposal-only / direction-only condition layer (degeneration framed by **fold geometry and
sign** only); **no** pressure (mmHg blocked), **no** glycaemic value (hba1c/mg-dl/mmol blocked), **no** length
(mm blocked), **no** staging/prognosis/risk magnitude, **no** '%'. The felt loss of sight is the mind
volume's.

**Next (same firewall, beyond the spine):** with the spine published and four mechanism extensions built
(E9 dichromacy, E10 adaptation, E11 accommodation/refraction, E12 acquired degeneration), the remaining
candidate is **SIX6** (eye-field TF), the one gene still in the atlas `_to_measure` — foldable by the
fetch→re-freeze discipline if a later increment needs it (it would deliberately re-freeze its inherited hash
and log the reason, per the no-regression rule). Absolute Hz at every rung stays **[O]**. The sibling
**hearing** sense ships as its own seed (`vp_ear_emergence_seed…`) — two files, two lanes.
